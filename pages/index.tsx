import React, { FC } from "react";
import Head from "next/head";
import Link from "next/link";
import Image from "next/image";

const Home = () => (
  <>
    <Head>
      <title>DTWM - Home</title>
    </Head>
    <h3>Welcome to the DTWM website :^)</h3>
    <Image width={200} height={200} src="images/skull/DTWMSkull.big.png" />
  </>
);

const title = "DTWM - Home";

export default Home;
