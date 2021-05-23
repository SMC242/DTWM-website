import React, { FC, PropsWithChildren, Children, ReactNode } from "react";
import { Circle, Tooltip, useColorModeValue } from "@chakra-ui/react";

import Arrow from "./arrow";

const select_angle = (children: number): ((index: number) => number) => {
  const ANGLES = [
    [180], // 1 child will be directly below the parent
    [195, 155], // 2 children will be offset from the middle by 25 degrees
    [195, 180, 155],
    [220, 195, 180, 155],
    [220, 195, 180, 155, 130],
    [220, 195, 180, 155, 130, 105],
    [255, 220, 195, 180, 155, 130, 105],
  ];
  const angle_set = ANGLES[children];
  return (index) => angle_set[index];
};

/**
 * The circumstances of a `Node` forming
 */
export type ChildNature = "SPLIT" | "MERGE";

export interface NodeProps {
  tag: string;
  name: string;
  alive?: boolean;
  /**
   * The nature of each child `Node`.
   * The length must match the length of the children.
   */
  child_types?: Array<ChildNature>;
}

const Node: FC<PropsWithChildren<NodeProps>> = ({
  tag,
  name,
  alive,
  child_types = [],
  children,
}) => {
  const number_of_children = Children.count(children);
  if (number_of_children !== child_types.length)
    throw new Error(
      "Number of children must be equal to the number of child types"
    );
  const get_angle = children ? select_angle(number_of_children) : () => 180; // I had to make a function so that get_angle would always be defined

  const color = useColorModeValue("black", "white");
  return (
    <>
      <Circle
        borderColor={color}
        borderStyle={alive ? "solid" : "dashed"}
        borderWidth="1px"
        p={2}
      >
        <Tooltip label={name} aria-label="outfit name">
          {tag}
        </Tooltip>
      </Circle>
      {Children.forEach(children, (child: ReactNode, index: number) => (
        <>
          <Arrow angle={get_angle(index)} />
          {child}
        </>
      ))}
    </>
  );
};

export default Node;
