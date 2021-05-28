import React, { FC } from "react";
import Head from "next/head";

export interface HeaderProps {
  site_name?: string;
  url?: string;
  description?: string;
  type?: string;
  image_url?: string;
  title?: string;
}

const Header: FC<HeaderProps> = ({
  site_name = "DTWM",
  url = "https://joindtwm.vercel.app/",
  description = "The DTWM weebs are invading your computer...",
  type = "website",
  image_url = "https://joindtwm.vercel.app/_next/image?url=%2Fimages%2Fskull%2FDTWMSkull.big.png&w=256&q=75",
  title = "DTWM",
}) => {
  console.log(site_name, url, description, type, image_url);
  return (
    <Head>
      <title>{title}</title>
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
      <meta property="og:site_name" content={site_name} key="ogsitename" />
      <meta property="og:url" content={url} key="ogurl" name="url" />
      <meta
        property="og:description"
        content={description}
        key="ogdesc"
        name="description"
      />
      <meta property="og:type" content={type} key="ogtype" name="type" />
      <meta
        property="og:image"
        content={image_url}
        key="ogimage"
        name="image"
      />
    </Head>
  );
};

export default Header;
