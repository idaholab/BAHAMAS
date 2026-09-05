# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import plotly.graph_objects as go
import plotly.io as pio

# pio.renderers.default = "browser"


def plot_histogram(data_dict, title, save=False, show=True):
  """Plot histogram for sampled data

  Args:
      data_dict (dict): dictionary of sampled data
      title (str): title for the plot
      save (bool, optional): Save plot into .png file if True (defaults to False)

  Returns:
    figure object: plotly figure object
  """
  hist_data = []
  for key, values in data_dict.items():
    hist_data.append(go.Histogram(x=values, name=key, opacity=0.75))
  # create a layout
  layout = go. Layout(
    title=dict(
      text=title,
      font=dict(size=24)
    ),
    barmode='overlay',
    xaxis=dict(
      title=dict(
        text='Occurrence Probability',
        font=dict(color='black', size=18)
      ),
      tickfont=dict(color='black', size=14)
    ),
    yaxis=dict(
      title=dict(
        text='Count',
        font=dict(color='black', size=18)
      ),
      tickfont=dict(color='black', size=14)
    ),
    legend=dict(
      font=dict(color='black', size=14)
    )
  )

  # layout = go.Layout(title=title, barmode='overlay', xaxis_title='Value', yaxis_title='Count')
  # create a figure
  fig = go.Figure(data=hist_data, layout=layout)
  # save the plot as image
  if save:
    fig.write_image(title+".png")

  if show:
    fig.show()
    # fig.write_html("my_plot.html", auto_open=True, full_html=True)

  return fig

