import React, { FC, useEffect } from "react";
import { pipe } from "ramda";
import Head from "next/head";

const redirection_meta = (url: string) =>
  Object.assign(document.createElement("meta"), {
    "http-equiv": "refresh",
    content: `0; URL='${url}'`,
  });

export interface RedirectorProps {
  url: string;
}

export const Redirector: FC<RedirectorProps> = ({ url }) => {
  return <Head>{redirection_meta}</Head>;
};
