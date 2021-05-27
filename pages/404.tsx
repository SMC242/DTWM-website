import React from "react";
import Head from "next/head";

const NotFoundPage = () => (
  <>
    <Head>
      <title>DTWM - 404</title>
    </Head>
    <h1>Status code: 404</h1>
    <small>Requested content not found :(</small>
  </>
);

export default NotFoundPage;
