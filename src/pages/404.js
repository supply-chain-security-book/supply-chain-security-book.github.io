import React from "react";
import Layout from "@rocketseat/gatsby-theme-docs/src/components/Layout";
import SEO from "@rocketseat/gatsby-theme-docs/src/components/SEO";

export default function NotFound() {
  return (
    <Layout title="ページが存在しません">
      <SEO title="404: Not found" />
      <p>Not found.</p>
    </Layout>
  );
}
