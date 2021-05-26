import React, { FC } from "react";
// @ts-ignore
import { Arrow as RArrow } from "react-arrow";

export interface ArrowProps {
  angle: number;
}

const Arrow: FC<ArrowProps> = ({ angle }) => {
  return <RArrow angle={angle} />;
};

export default Arrow;
