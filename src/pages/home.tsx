import React, { FC } from "react";
import { PageTemplate } from "../components/templates/page_template";

const Body = () => (
  <div>
    <h3>Welcome to the DTWM website :^)</h3>
  </div>
);

const title = "DTWM - Home";

export const Home = () => <PageTemplate title={title} body={<Body />} />;
