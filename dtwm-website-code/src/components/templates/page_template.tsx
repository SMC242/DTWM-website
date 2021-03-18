import React, { FC, ReactNode } from "react";
import Helmet from "react-helmet";

export interface PageTemplateProps {
  title?: string;
  head?: ReactNode;
  body: ReactNode;
}

export const PageTemplate: FC<PageTemplateProps> = ({ title, head, body }) => {
  return (
    <>
      <Helmet>
        <title>{title}</title>
        <head>{head}</head>
      </Helmet>
      <>{body}</>
    </>
  );
};
