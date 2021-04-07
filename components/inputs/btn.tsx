import React, { FC } from "react";
import { Button, ButtonProps, useStyleConfig } from "@chakra-ui/react";

export const MainButton: FC<ButtonProps> = (props) => {
  const { size, variant, children, ...rest } = props;
  const styles = useStyleConfig("MainButton", { size, variant });

  return (
    <Button
      bgGradient={styles["bgGradient"] as string}
      bg={styles["bg"] as string}
      {...rest}
    >
      {children}
    </Button>
  );
};
