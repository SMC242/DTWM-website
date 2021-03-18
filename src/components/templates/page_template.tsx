import React, { FC, ReactNode } from "react";
import Helmet from "react-helmet";
import Skull from "../../images/skull/skull32.png";

const get_link = (icon: HTMLLinkElement | undefined) =>
  icon || <link rel="shortcut icon" type="image/x-icon" href={Skull} />;

export interface PageTemplateProps {
  title?: string;
  head?: ReactNode;
  body: ReactNode;
  /**
   * Defaults to the DTWM skull
   */
  icon?: HTMLLinkElement;
}

export const PageTemplate: FC<PageTemplateProps> = ({
  title,
  head,
  body,
  icon,
}) => {
  return (
    <>
      <Helmet>
        <title>{title}</title>
        <head>{head}</head>
        {get_link(icon)}
      </Helmet>
      <>{body}</>
    </>
  );
};
