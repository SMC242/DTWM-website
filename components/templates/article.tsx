import React, { FC, PropsWithChildren, ReactNode } from "react";
import {
  Grid,
  Container,
  Box,
  ContainerProps,
  useStyleConfig,
} from "@chakra-ui/react";

export interface ArticleProps extends ContainerProps {
  LeftSidebar?: ReactNode;
  RightSidebar?: ReactNode;
}

const Artcle: FC<PropsWithChildren<ArticleProps>> = ({
  children,
  size,
  variant,
  LeftSidebar = <Box />,
  RightSidebar = <Box />,
  ...props
}) => {
  const article_style = useStyleConfig("Article", { size, variant });

  return (
    <Grid templateColumns="1fr 4fr 1fr" gap={0}>
      {LeftSidebar}
      <Container sx={article_style}>
        <Container {...props}>{children}</Container>
      </Container>
      {RightSidebar}
    </Grid>
  );
};

export default Artcle;
