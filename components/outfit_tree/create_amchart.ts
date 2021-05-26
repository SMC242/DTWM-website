/* Imports */
import {
  create,
  useTheme,
  Sprite,
  DropShadowFilter,
} from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import {
  ForceDirectedTree,
  ForceDirectedSeries,
} from "@amcharts/amcharts4/plugins/forceDirected";

import am4themes_dark from "@amcharts/amcharts4/themes/dark";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

useTheme(am4themes_dark);
useTheme(am4themes_animated);

/**
 * The first parent outfit.
 * Its child outfits should be held in `children`
 */
export interface TreeNode {
  tag: string;
  name: string;
  children: Array<TreeNode>;
  /**
   * An identifier for linking to
   */
  id: string;
  /**
   * A list of IDs to link to.
   */
  links: Array<string>;
}

interface ChartItem {
  name: string; // the outfit tag
  value: number; // will always be 1
  outfit_name: string;
  children: Array<ChartItem>;
  id: string;
  links: Array<string>;
}

/**
 * Recursively convert a tree to a form that can be used with `amcharts`
 * @param node The tree to convert
 * @returns The `ChartItem`s
 */
const ChartItemFactory = (node: TreeNode): ChartItem => ({
  name: node.tag,
  outfit_name: node.name,
  children: node.children.map((n) => ChartItemFactory(n)),
  value: 1,
  id: node.id,
  links: node.links,
});

const make_chart_ready = (tree: TreeNode): [ChartItem] => {
  return [ChartItemFactory(tree)];
};

const get_series = (chart: ForceDirectedTree): ForceDirectedSeries =>
  chart.series.push(new ForceDirectedSeries());

const set_data =
  (data: Array<ChartItem>) =>
  (series: ForceDirectedSeries): ForceDirectedSeries => {
    series.data = data;
    return series;
  };

/**
 * Set up the fields and labels for the chart.
 */
const set_fields = (series: ForceDirectedSeries): ForceDirectedSeries => {
  const keys = {
    value: "value",
    name: "name",
    children: "children",
    outfit_name: "outfit_name",
    id: "id",
    linkWith: "links",
  };
  series.dataFields = { ...series.dataFields, ...keys };
  series.nodes.template.label.text = "{name}";
  series.nodes.template.tooltipText = "[[{name}]] {outfit_name}";
  return series;
};

const customise_series = (series: ForceDirectedSeries): ForceDirectedSeries => {
  series.nodes.template.outerCircle.filters.push(new DropShadowFilter()); // Add a nice shadow
  return series;
};

const customise_chart = (chart: ForceDirectedTree): ForceDirectedTree => {
  chart.zoomable = true;
  return chart;
};

/**
 * Create a tree of outfits
 * @param chart_id The id of the element to mount the chart into.
 * @returns [the chart, the unmount callback]
 */
export const create_outfit_tree =
  (chart_id: string) =>
  (nodes: TreeNode): [Sprite, () => void] => {
    const set_up_chart = (chart: ForceDirectedTree) =>
      set_fields(customise_series(get_series(chart)));
    const chart = create(chart_id, ForceDirectedTree);
    customise_chart(chart);
    const series = set_up_chart(chart);
    set_data(make_chart_ready(nodes))(series);
    return [chart, () => chart.dispose()];
  };