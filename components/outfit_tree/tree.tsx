import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import React, { FC, PropsWithChildren } from "react";
import { Box, Circle, useColorModeValue } from "@chakra-ui/react";

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
            <Circle borderColor={color} borderStyle="solid" borderWidth="1">
              Alive outfit
            </Circle>
            <Circle borderColor={color} borderStyle="dashed" borderWidth="1">
              Dead outfit
            </Circle>
          </Box>
          {children}
        </Box>
      </TransformComponent>
    </TransformWrapper>
  );
};

export default Tree;
