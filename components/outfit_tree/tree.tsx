import React, { FC, useEffect, useState } from "react";
import { Box } from "@chakra-ui/react";

import { create_outfit_tree, TreeNode } from "./create_amchart";

export interface TreeProps {
  nodes: TreeNode;
  title?: string;
}

type ChartType = ReturnType<ReturnType<typeof create_outfit_tree>>[0];

const Tree: FC<TreeProps> = ({ nodes, title }) => {
  const [tree, set_tree] = useState<null | ChartType>(null);
  const chart_title = title || `${nodes["tag"]} family tree`;
  useEffect(() => {
    const [_tree, unmount] = create_outfit_tree(chart_title)(nodes);
    set_tree(_tree);
    return unmount;
  });
  return <Box id={chart_title}>{tree}</Box>;
};

export default Tree;
