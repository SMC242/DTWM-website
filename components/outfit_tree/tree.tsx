import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import React, { FC, PropsWithChildren } from "react";
import { Box, useColorModeValue } from "@chakra-ui/react";

import NodeCircle from "./node_circle";

export interface TreeProps {}

const Tree: FC<PropsWithChildren<TreeProps>> = ({ children }) => {
  const color = useColorModeValue("black", "white");
  return (
    <TransformWrapper>
      <TransformComponent>
        <Box bg="transparent">
          <Box
            float="right"
            borderColor={color}
            borderWidth="2px"
            p={2}
            marginLeft={2}
          >
            <u>Key</u>
            <NodeCircle alive>Alive outfit</NodeCircle>
            <NodeCircle alive={false}>Dead outfit</NodeCircle>
          </Box>
          {children}
        </Box>
      </TransformComponent>
    </TransformWrapper>
  );
};

export default Tree;
