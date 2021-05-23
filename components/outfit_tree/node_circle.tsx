import React, { FC, PropsWithChildren } from "react";
import { Circle, useColorModeValue } from "@chakra-ui/react";

export interface NodeCircleProps {
  alive: boolean;
}

const NodeCircle: FC<PropsWithChildren<NodeCircleProps>> = ({
  alive,
  children,
}) => {
  const color = useColorModeValue("black", "white");
  return (
    <Circle
      borderColor={color}
      borderStyle={alive ? "solid" : "dashed"}
      borderWidth="1px"
      p={2}
      m={1}
    >
      {children}
    </Circle>
  );
};

export default NodeCircle;
