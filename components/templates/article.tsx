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
  LeftSidebar,
  RightSidebar,
  ...props
}) => {
  const article_style = useStyleConfig("Article", { size, variant });
  const Left = LeftSidebar || <Box />;
  const Right = RightSidebar || <Box />;

  return (
    <Grid templateColumns="1fr 4fr 1fr" gap={0}>
      {Left}
      <Container sx={article_style}>
        <Container {...props}>{children}</Container>
      </Container>
      {Right}
    </Grid>
  );
};

export default Artcle;
