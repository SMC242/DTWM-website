import React, { FC, useEffect, useState } from "react";
import { Box } from "@chakra-ui/react";

import { create_outfit_tree, TreeNode } from "./create_amchart";

export interface TreeProps {
  nodes: TreeNode;
  title?: string;
}

type ChartType = ReturnType<typeof create_outfit_tree>;

const Tree: FC<TreeProps> = ({ nodes, title }) => {
  const [tree, set_tree]: [null | ChartType, () => void] = useState(null);
  const chart_title = title || `${nodes["tag"]} family tree`;
  useEffect(() => {
    const [tree, unmount] = create_outfit_tree(chart_title)(nodes);
    return unmount;
  });
  return <Box id="">{tree}</Box>;
};

export default Tree;
