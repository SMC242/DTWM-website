import "../styles/globals.css";
import React, { FC } from "react";
import type { AppProps } from "next/app";
import Head from "next/head";
import { CustomChakraProvider } from "../theme";
import { HNavbar } from "../components/navigation/navbar";

const MyApp: FC<AppProps> = ({ Component, pageProps }) => {
  const links = [
    {
      text: "Home",
      route: "/",
    },
    {
      text: "Info",
      route: "/info",
    },
    {
      text: "Discord",
      route: "https://joindtwm.vercel.app/join",
    },
    {
      text: "Training Docs",
      route: "/training/training-home",
    },
  ];

  return (
    <CustomChakraProvider>
      <Head>
        {/* favicon stuff */}
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
        <meta name="msapplication-TileColor" content="#9f00a7" />
        <meta name="theme-color" content="#e60ded" />

        {/* OpenGraph stuff */}
        <meta property="og:site_name" content="DTWM" key="ogsitename" />
        <meta
          property="og:url"
          content="https://joindtwm.vercel.app/"
          key="ogurl"
        />
        <meta
          property="og:description"
          content="The DTWM weebs are invading your computer..."
          key="ogdesc"
        />
        <meta property="og:type" content="website" key="ogtype" />
        <meta
          property="og:image"
          content="https://joindtwm.vercel.app/_next/image?url=%2Fimages%2Fskull%2FDTWMSkull.big.png&w=256&q=75"
          key="ogimage"
        />
      </Head>
      <HNavbar links={links} />
      <Component {...pageProps} />
    </CustomChakraProvider>
  );
};

export default MyApp;
