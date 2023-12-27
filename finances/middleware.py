from django.urls import reverse


class MenuItem:
    def __init__(self, label, url, submenu=None, disabled=False):
        self.label = label
        self.url = url
        self.submenu = submenu
        self.has_submenu = submenu is not None
        self.disabled = disabled

    def __str__(self):
        return self.label


class MenuMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        menu_data = [
            MenuItem('Home', reverse('finances:home')),
            MenuItem(
                'Finances',
                '#',
                submenu=[
                    MenuItem('Incomes', reverse('finances:income_index')),
                    MenuItem('Expenses', reverse('finances:expense_index')),
                ],
            ),
            MenuItem(
                'Reports',
                '#',
                submenu=[
                    MenuItem('Report 1', '#'),
                    MenuItem('Report 2', '#'),
                ],
                disabled=True,
            ),
            MenuItem(
                'Planning',
                '#',
                submenu=[
                    MenuItem('Budget', '#'),
                    MenuItem('Investment', '#'),
                ],
                disabled=True,
            ),
        ]

        # Adicione a variável menu_data ao contexto global
        request.menu_data = menu_data
        # print('----> Len', len(menu_data[1].submenu), menu_data[1].has_submenu,menu_data[1].submenu.items())
        response = self.get_response(request)
        return response
