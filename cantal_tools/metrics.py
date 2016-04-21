from ._fork import Fork

__all__ = [
    'wsgi',
    'web',
    'appflow',
    ]

wsgi = Fork(state='wsgi')

web = Fork(state='web')

appflow = Fork(state='appflow')
