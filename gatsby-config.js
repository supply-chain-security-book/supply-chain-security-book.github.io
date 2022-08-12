module.exports = {
  siteMetadata: {
    siteTitle: "TODO",
    defaultTitle: "TODO",
    siteTitleShort: "TODO",
    siteDescription: "TODO",
    siteUrl: "https://chainsec.shift-js.info",
    siteAuthor: "@lmt_swallow",
    siteImage: "/banner.png",
    siteLanguage: "ja",
    themeColor: "#8257E6",
    basePath: "/",
  },
  flags: { PRESERVE_WEBPACK_CACHE: true },
  plugins: [
    {
      resolve: "@rocketseat/gatsby-theme-docs",
      options: {
        configPath: "src/config",
        docsPath: "src/docs",
        repositoryUrl:
          "https://github.com/supply-chain-security-book/supply-chain-security-book.github.io",
        baseDir: "",
        withMdx: false,
      },
    },
    {
      resolve: `gatsby-plugin-mdx`,
      options: {
        extensions: [`.mdx`, `.md`],
        remarkPlugins: [require("remark-emoji")],
        gatsbyRemarkPlugins: [
          `gatsby-remark-autolink-headers`,
          `gatsby-remark-embedder`,
          {
            resolve: `gatsby-remark-images`,
            options: {
              maxWidth: 440,
              withWebp: true,
              linkImagesToOriginal: false,
            },
          },
          `gatsby-remark-numbered-footnotes`,
          `gatsby-remark-responsive-iframe`,
          `gatsby-remark-copy-linked-files`,
        ],
        plugins: [`gatsby-remark-autolink-headers`, `gatsby-remark-images`],
      },
    },
    "gatsby-plugin-sitemap",
    "gatsby-plugin-remove-trailing-slashes",
    {
      resolve: "gatsby-plugin-canonical-urls",
      options: {
        siteUrl: "https://chainsec.shift-js.info",
      },
    },
    "gatsby-plugin-offline",
    {
      resolve: "gatsby-plugin-typegen",
      options: {
        outputPath: `src/@types/gatsby-types.d.ts`,
      },
    },
    {
      resolve: `gatsby-plugin-google-gtag`,
      options: {
        trackingIds: ["G-KEE2K7WXT7"],
      },
    },
  ],
};
