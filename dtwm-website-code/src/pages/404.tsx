import React from "react";
import { PageTemplate } from "../components/templates/page_template";

const Body = () => (
  <>
    <h1>Status code: 404</h1>
    <small>Requested content not found :(</small>
  </>
);

const title = "DTWM - 404";

export const NotFoundErrorPage = () => (
  <PageTemplate title={title} body={<Body />} />
);
