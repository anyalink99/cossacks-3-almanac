// Chart.js wrappers for resource curves & population.

import { RES_INFO, RES_ORDER, fmtTime } from "./i18n.js";

const COLORS = {
  food:  "#d97766",
  wood:  "#a06f3b",
  stone: "#9b8a6a",
  gold:  "#d4a857",
  iron:  "#6da5d4",
  coal:  "#4a3b27",
};

let resourceChart = null, popChart = null;

export function renderResources(snapshots) {
  const ctx = document.getElementById("chart_resources").getContext("2d");
  const labels = snapshots.map(s => s.t_g);
  const datasets = RES_ORDER.map(k => ({
    label: RES_INFO[k].ru,
    data: snapshots.map(s => s[`res_${k}`]),
    borderColor: RES_INFO[k].color,
    backgroundColor: RES_INFO[k].color + "22",
    borderWidth: 1.6,
    pointRadius: 0,
    fill: false,
    tension: 0.18,
  }));
  if (resourceChart) resourceChart.destroy();
  resourceChart = new Chart(ctx, {
    type: "line",
    data: { labels, datasets },
    options: chartOpts(),
  });
}

export function renderPop(snapshots) {
  const ctx = document.getElementById("chart_pop").getContext("2d");
  const labels = snapshots.map(s => s.t_g);
  if (popChart) popChart.destroy();
  popChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Крестьяне", data: snapshots.map(s => s.peasants_total),
          borderColor: "#87b369", backgroundColor: "#87b36922", borderWidth: 1.8,
          pointRadius: 0, tension: 0.18 },
        { label: "Ферма (used)", data: snapshots.map(s => s.farm_used),
          borderColor: "#d4a857", borderWidth: 1.4, pointRadius: 0, tension: 0.18 },
        { label: "Ферма (cap)", data: snapshots.map(s => s.farm_cap),
          borderColor: "#4a3b27", borderWidth: 1.2, borderDash: [5,5],
          pointRadius: 0, tension: 0 },
      ],
    },
    options: chartOpts({ beginAtZero: true }),
  });
}

function chartOpts(yOpts = {}) {
  return {
    animation: false,
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: "index", intersect: false },
    scales: {
      x: {
        ticks: { color: "#8a7d62", maxTicksLimit: 8 },
        grid: { color: "#2a2218" },
        title: { display: true, text: "g-сек", color: "#8a7d62", font: { size: 11 } },
      },
      y: {
        ticks: { color: "#8a7d62" },
        grid: { color: "#2a2218" },
        ...yOpts,
      },
    },
    plugins: {
      legend: {
        labels: { color: "#cfd2d8", boxWidth: 12, boxHeight: 12, padding: 10, font: { size: 11 } },
        position: "top",
      },
      tooltip: {
        backgroundColor: "#1a1610",
        titleColor: "#d4a857",
        bodyColor: "#e5dcc6",
        borderColor: "#3a2e1f",
        borderWidth: 1,
      },
    },
  };
}
