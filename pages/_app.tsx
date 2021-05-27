import "../styles/globals.css";
import React, { FC } from "react";
import type { AppProps } from "next/app";
import Head from "next/head";
import { CustomChakraProvider } from "../theme";
import { HNavbar } from "../components/navigation/navbar";
import OG from "../components/templates/open_graph";

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
    { text: "Outfit Trees", route: "/outfit_trees/outfit_trees_home" },
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

        <OG />
      </Head>
      <HNavbar links={links} />
      <Component {...pageProps} />
    </CustomChakraProvider>
  );
};

export default MyApp;
