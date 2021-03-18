import React, { FC } from "react";
import { Link } from "../../pages/routes";

export interface CustomLinkProps {
  route_name: string;
}

const CustomLink: FC<CustomLinkProps> = ({ route_name }) => (
  <Link route={route_name} passHref />
);
