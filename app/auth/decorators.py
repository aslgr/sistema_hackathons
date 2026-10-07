from functools import wraps

from flask import flash, g, redirect, url_for


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.usuario is None:
            flash("Faça login para acessar esta página.")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def role_required(*papeis):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.usuario is None:
                flash("Faça login para acessar esta página.")
                return redirect(url_for("auth.login"))

            if g.usuario.papel not in papeis:
                flash("Você não tem permissão para acessar esta página.")
                return redirect(url_for("index"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator
