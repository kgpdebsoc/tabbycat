from django.utils.datastructures import SortedDict

#name,  coerce, help, default
SETTINGS = SortedDict([
    ('score_min', (int, 'Minimum allowed score', 68)),
    ('score_max', (int, 'Maximum allowed score', 82)),
    ('reply_score_min', (int, 'Minimum allowed reply score', 34)),
    ('reply_score_max', (int, 'Maximum allowed reply score', 41)),
    ('break_size', (int, 'Number of breaking teams', 16)),
    ('adj_min_score', (float, 'Minimum adjudicator score', 1.5)),
    ('adj_max_score', (float, 'Maximum adjudicator score', 5)),
    ('adj_chair_min_score', (float, 'Minimum chair score', 3.5)),
    ('adj_conflict_penalty', (int, 'Penalty for adjudicator-team conflict',
                              1000000)),
    ('adj_history_penalty', (int, 'Penalty for adjudicator-team history',
                              10000)),
])


class Config(object):
    def __init__(self, tournament):
        self._t = tournament

    def __getattr__(self, key):
        return self.get(key)

    def get(self, key):
        from debate.models import Config
        if key in SETTINGS:
            coerce, help, default = SETTINGS[key]
            return coerce(Config.objects.get_(self._t, key, default))

    def set(self, key, value):
        from debate.models import Config
        Config.objects.set(self._t, key, value)


def make_config_form(tournament, data=None):
    from django import forms

    def _field(t):
        if t is int:
            return forms.IntegerField
        if t is float:
            return forms.FloatField

    fields = SortedDict()
    initial_data = {}
    for name, (coerce, help, default) in SETTINGS.items():
        fields[name] = _field(coerce)(help_text=help)
        fields[name].default = default
        initial_data[name] = tournament.config.get(name)
    class BaseConfigForm(forms.BaseForm):
        def save(self):
            for name in SETTINGS.keys():
                tournament.config.set(name, self.cleaned_data[name])

    klass = type('ConfigForm', (BaseConfigForm,), {'base_fields': fields})
    if not data:
        return klass(initial=initial_data)
    else:
        return klass(data)

