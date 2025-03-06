from django.shortcuts import redirect


# middleware
def auth_middleware(get_response):
    def middleware(request):
        if not request.user.is_authenticated:
            returnUrl = request.META["PATH_INFO"]
            if not request.session.get("customer_id"):
                request.session["return_to"] = returnUrl
                return redirect(f"login?return_url={returnUrl}")
        else:
            request.session["return_to"] = request.path
        response = get_response(request)
        return response

    return middleware

# middleware (decorator)
def unauthentcated_user(view_func):
    def middlerware_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return middlerware_func
