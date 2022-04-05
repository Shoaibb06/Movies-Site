import stripe
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import *
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

base_url = 'https://api.themoviedb.org/3/'

stripe.api_key = settings.STRIPE_SECRET_KEY


def success_view(request):
    return redirect('index')


class CancelView(TemplateView):
    template_name = 'cancel.html'


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=[
                    'card',
                ],
                line_items=[
                    {
                        # TODO: replace this with the `price` of the product you want to sell
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 1000,
                            'product_data': {
                                'name': 'Movie Star Subscription',
                            }
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'http://{request.get_host()}/success/',
                cancel_url=f'http://{request.get_host()}/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return str(e)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    update_subscription(session)


def update_subscription(session):
    user_email = session["customer_details"]["email"]
    try:
        user = User.objects.get(email=user_email)
        # update coins here
    except Exception:
        msg = "User does not exist"


def index(request):
    movies = Movie.objects.only('title', 'poster_url')
    paginator = Paginator(movies, 24)

    page = request.GET.get('page')
    if page is None:
        page = '1'
    movies = paginator.get_page(page)
    num_pages = movies.paginator.num_pages
    nums = list(range(int(page), (int(page) + 3) % num_pages))
    page = 'index'

    context = {
        'movies': movies,
        'nums': nums,
        'page': page,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'index.html', context=context)


def genres(request):
    movies = Movie.objects.all()
    genres = []
    ids = []
    for movie in movies:
        for genre in movie.genres:
            a = 3
            if genre['name'] in ['Documentary', 'Family', 'Foreign', 'History', 'Music', 'TV Movie', 'Western', 'War']:
                ids.append(movie.id)
            else:
                genres.append(genre['name'])

    genres = list(set(genres))
    genres.sort()
    print(ids)
    return render(request, 'genres.html', {'genres': genres})


def movie_list(request, genre):
    movies = Movie.objects.only('title', 'poster_url')
    movie_list = []
    for movie in movies:
        for g in movie.genres:
            a = 3
            if g['name'] == genre:
                movie_list.append(movie)

    paginator = Paginator(movie_list, 24)
    page = request.GET.get('page')
    if page == None:
        page = '1'
    movie_list = paginator.get_page(page)
    num_pages = movie_list.paginator.num_pages
    if int(page) >= num_pages - 3:
        page = num_pages - 2
    nums = list(range(int(page), (int(page) + 3)))
    return render(request, 'movies_by_genre.html', {'movies': movie_list, 'nums': nums, 'genre': genre})


def movie_details(request, movie_id):
    movie = Movie.objects.filter(pk=movie_id)
    genres = []
    try:
        rating = Rating.objects.filter(user=request.user, movie=movie[0]).last().rating
    except Exception:
        rating = None
    try:
        movie_rating = Rating.objects.filter(movie=movie[0]).aggregate(Sum('rating'))['rating__sum']
        movie_rating_count = Rating.objects.filter(movie=movie[0]).count()
        movie_rating = round(movie_rating / movie_rating_count, 2)
        rating_one = round(Rating.objects.filter(movie=movie[0], rating=1).count() / movie_rating_count * 100, 2)
        rating_two = round(Rating.objects.filter(movie=movie[0], rating=2).count() / movie_rating_count * 100, 2)
        rating_three = round(Rating.objects.filter(movie=movie[0], rating=3).count() / movie_rating_count * 100, 2)
        rating_four = round(Rating.objects.filter(movie=movie[0], rating=4).count() / movie_rating_count * 100, 2)
        rating_five = round(Rating.objects.filter(movie=movie[0], rating=5).count() / movie_rating_count * 100, 2)
    except Exception:
        movie_rating = 0
        movie_rating_count = 0
        rating_one = 0
        rating_two = 0
        rating_three = 0
        rating_four = 0
        rating_five = 0
    for genre in movie[0].genres:
        genres.append(genre['name'])
    if movie:
        return render(request, 'movie_details.html',
                      {'movie': movie[0], 'genres': genres, 'rating': rating, 'movie_rating': movie_rating,
                       'movie_rating_count': movie_rating_count, 'rating_one': rating_one, 'rating_two': rating_two,
                       'rating_three': rating_three, 'rating_four': rating_four, 'rating_five': rating_five, })
    else:
        return render(request, '404_page.html')


@csrf_exempt
def submit_rating(request):
    try:
        rating_obj = Rating()
        rating_obj.user_id = request.user.id
        rating_obj.movie_id = int(request.POST.get('movie_id'))
        rating_obj.rating = int(request.POST.get('rating'))
        rating_obj.save()
    except Exception:
        error = True
    else:
        error = False
    print(error)
    data = {
        'error': error,
    }
    return JsonResponse(data)
