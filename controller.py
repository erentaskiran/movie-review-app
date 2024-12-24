__all__ = ['FilmController', 'setup_page1_bindings', 'setup_page2_bindings']

import json
import tkinter as tk
from tkinter import ttk


class FilmController:
    def __init__(self):
        self.films = self.load_films()

    def load_films(self):
        try:
            with open('films.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def filter_films(self, film_name=None, film_type=None, watch_status=None, min_rating=None, max_rating=None):
        filtered = self.films

        if film_name:
            filtered = [f for f in filtered if film_name.lower()
                        in f['name'].lower()]

        if film_type:
            filtered = [f for f in filtered if film_type.lower()
                        in f['type'].lower()]

        if watch_status:
            filtered = [f for f in filtered if f['status'] == watch_status]

        if min_rating:
            try:
                min_rating = float(min_rating)
                filtered = [f for f in filtered if f['rating'] >= min_rating]
            except ValueError:
                pass

        if max_rating:
            try:
                max_rating = float(max_rating)
                filtered = [f for f in filtered if f['rating'] <= max_rating]
            except ValueError:
                pass

        return filtered


def setup_page1_bindings(page1):
    controller = FilmController()

    def update_tree(filtered_films):
        for item in page1.tree.get_children():
            page1.tree.delete(item)

        for film in filtered_films:
            page1.tree.insert('', 'end', values=(
                film.get('name', ''),
                film.get('type', ''),
                film.get('watch_status', ''),
                film.get('rating', ''),
                film.get('review', '')
            ))

    def on_filter_change(*args):
        film_name = page1.name_var.get().lower()
        film_type = page1.type_var.get().lower()
        watch_status = page1.status_var.get().lower()
        min_rating = page1.min_rating_var.get()
        max_rating = page1.max_rating_var.get()

        filtered_films = controller.filter_films(
            film_name=film_name,
            film_type=film_type,
            watch_status=watch_status,
            min_rating=min_rating if min_rating else None,
            max_rating=max_rating if max_rating else None
        )

        update_tree(filtered_films)

    for var in [page1.name_var, page1.type_var, page1.status_var,
                page1.min_rating_var, page1.max_rating_var]:
        var.trace_add('write', on_filter_change)

    update_tree(controller.load_films())


def setup_page2_bindings(page2):
    controller = FilmController()

    def save_film():
        film_data = {
            'name': page2.children['!entry'].get(),
            'type': page2.children['!entry2'].get(),
            'status': page2.children['!entry3'].get(),
            'review': page2.children['!entry4'].get(),
            'rating': float(page2.children['!entry5'].get() or 0),
            'genre': page2.children['!entry6'].get(),
            'watch_status': page2.children['!entry7'].get()
        }

        try:
            with open('films.json', 'r', encoding='utf-8') as f:
                films = json.load(f)
        except FileNotFoundError:
            films = []

        films.append(film_data)

        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(films, f, ensure_ascii=False, indent=4)

        print("Film başarıyla kaydedildi!")

        for entry in page2.children.values():
            if isinstance(entry, ttk.Entry):
                entry.delete(0, 'end')

        page2.master.select(0)

    page2.children['!button'].configure(command=save_film)
