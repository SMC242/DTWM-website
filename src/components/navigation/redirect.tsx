import React, { FC, useEffect } from "react";
import { pipe } from "ramda";

// Functions to edit the head
const create_head = () => {
  const head = document.createElement("head");
  const doc = document.querySelector("html");
  if (!doc)
    throw new Error(
      "Redirector: There is no HTML tag. How the hell did you manage this?"
    );
  doc.appendChild(head);
  return head;
};

const get_head = () => document.querySelector("head") || create_head();
const edit_head = (head: HTMLHeadElement) => (e: Element) =>
  head.appendChild(e);
const add_to_head = pipe(get_head, edit_head)();

const redirection_meta = (url: string) =>
  Object.assign(document.createElement("meta"), {
    "http-equiv": "refresh",
    content: `0; URL='${url}'`,
  });

export interface RedirectorProps {
  url: string;
}

export const Redirector: FC<RedirectorProps> = ({ url }) => {
  // Add the redirection on mount
  useEffect(() => {
    add_to_head(redirection_meta(url));
  });
  return <div id={`Redirector?url=${url}`}></div>;
};
