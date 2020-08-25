import os

from django.conf import settings


class TestWorkflow:

    def test_workflow(self):
        try:
            with open(f'{os.path.join(settings.BASE_DIR, "yamdb.yaml")}', 'r') as f:
                yamdb = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл yamdb.yaml в корневой каталог для проверки'

        assert 'on: [push]' in yamdb, 'Проверьте, что добавили действие при пуше в файл yamdb.yaml'
        assert 'flake8 .' in yamdb, 'Проверьте, что добавили проверку flake8 в файл yamdb.yaml'
        assert 'pytest' in yamdb, 'Проверьте, что добавили pytest в файл yamdb.yaml'
        assert 'docker/build-push-action' in yamdb, 'Проверьте, что добавили доставку докер-образаов в Docker Hub ' \
                                                    'в файл yamdb.yaml'
