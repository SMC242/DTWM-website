import React, { FC } from "react";
import { Button, ButtonProps, useColorModeValue } from "@chakra-ui/react";

export const MainButton: FC<ButtonProps> = (props) => {
  const gradient = useColorModeValue(
    "linear(to-t, yellow.500, orange.300)",
    "linear(to-b, pink.500, purple.500)"
  );
  const bg = useColorModeValue(undefined, "unset");

  return (
    <Button
      bgGradient={props.bgGradient || gradient}
      background={props.bg || bg}
      _hover={{ filter: "invert(100%)" }}
      {...props}
    >
      {props.children}
    </Button>
  );
};
