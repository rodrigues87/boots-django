import random

from django.contrib.auth.admin import UserAdmin
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


from cadastros.models import Cadastros
from cursos.models import Turmas
from pagamentos.models import Pagamentos
from vendas.models import Venda
from .counters import CounterBase
from .charts import ChartsBase


class ValiDashboardBase(TemplateView):
  extra_context_data = []
  list_counters = []
  list_charts = []

  def get_list_counters(self):
    list_counters = []
    for counter in self.list_counters:
      if isinstance(counter, CounterBase):
        list_counters.append(
          {
            'title': counter.get_title(self.request),
            'value': counter.get_value(self.request),
            'style': counter.get_style(self.request),
            'icon': counter.get_icon(self.request),
          }
        )
      else:
        list_counters.append(counter)
    return list_counters

  def get_list_charts(self):
    list_charts = []
    for chart in self.list_charts:
      if isinstance(chart, ChartsBase):
        list_charts.append(
          {
            'title': chart.get_title(self.request),
            'name': chart.get_name(self.request),
            'chart_type': chart.get_chart_type(self.request),
            'labels': chart.get_labels(self.request),
            'datasets': chart.get_datasets(self.request),
          }
        )
      else:
        list_charts.append(chart)
    return list_charts

  def get_extra_context_data(self):
    return self.extra_context

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['counters'] = self.get_list_counters()
    context['charts'] = self.get_list_charts()
    return context

  def get_template_names(self):
    return super().get_template_names()

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super(ValiDashboardBase, self).dispatch(request, *args, **kwargs)


def usuariosAtivos():
  count = 0

  cadastros = Cadastros.objects.all()

  for cadastro in cadastros:
    try:
      Turmas.objects.filter(alunos=cadastro)
      count = count + 1

    except Turmas.DoesNotExist:
      pass

  return count


def usuariosInativos():
  cadastrosTotais = Cadastros.objects.count()
  count = cadastrosTotais - usuariosAtivos()
  return count


def pagamentosAberto():
  result = Pagamentos.objects.filter(pago=False)
  return result.count()


def vendas():
  quantidadeVendas = Venda.objects.count()
  return quantidadeVendas


class ValiDashboardView(ValiDashboardBase):

  r = lambda: random.randint(0, 100)

  template_name = 'dashboard.html'
  # default count users data
  users = usuariosAtivos()
  # default count groups data
  userInat = usuariosInativos()
  # default count apps data
  pagamentosEmAberto = pagamentosAberto()

  vendas = vendas()
  # default charts data
  list_charts = [

    {
      # Support Chart types: PolarArea, Pie, Doughnut
      "name": "piechart1",
      "title": "Faltas",
      "chart_type": "Pie",
      "datasets": [

        {
          "value": 300,
          "color": '#%02X%02X%02X' % (r(), r(), r()),
          "label": "Red"
        },
        {
          "value": 50,
          "color": '#%02X%02X%02X' % (r(), r(), r()),
          "label": "Green"
        },
        {
          "value": 100,
          "color": '#%02X%02X%02X' % (r(), r(), r()),
          "label": "Yellow"
        },
      ]
    },
    {
      # Support Chart types: Bar, Line, Radar
      "name": "vendas",
      "title": "Vendas Mensais",
      "chart_type": "Bar",
      "labels": ["2018-03-01", "2018-03-02", "2018-03-03", "2018-03-04", "2018-03-05"],
      "datasets": [
        {
          "label": "dataset 1",
          "fillColor": "rgba(220,220,220,0.2)",
          "strokeColor": "rgba(220,220,220,1)",
          "pointColor": "rgba(220,220,220,1)",
          "pointStrokeColor": "#fff",
          "pointHighlightFill": "#fff",
          "pointHighlightStroke": "rgba(220,220,220,1)",
          "data": [65, 59, 80, 81, 80]
        },
        {
          "label": "dataset 2",
          "fillColor": "rgba(151,187,205,0.2)",
          "strokeColor": "rgba(151,187,205,1)",
          "pointColor": "rgba(151,187,205,1)",
          "pointStrokeColor": "#fff",
          "pointHighlightFill": "#fff",
          "pointHighlightStroke": "rgba(151,187,205,1)",
          "data": [28, 48, 40, 19, 69]
        }
      ],
    },

  ]

  # default icons data
  list_counters = [
    {"title": "ATIVOS", "value": users, "style": "primary", "icon": "fa-user-circle"},
    {"title": "INATIVOS", "value": userInat, "style": "warning", "icon": "fa-users"},
    {"title": "PENDENTES", "value": pagamentosEmAberto, "style": "info", "icon": "fa-money"},
    {"title": "VENDAS", "value": vendas, "style": "danger", "icon": "fa-line-chart"},
  ]


class ValiChangePassword(UserAdmin):
  template_name = "admin/auth/user/change_password.html"

