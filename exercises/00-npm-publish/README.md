# Try `npm publish`

## Createa Your Own Package

Edit `name` of `./the-most-fancy-package-ever/package.json`, then edit `./the-most-fancy-package-ever/index.js` as you like.

## Publish Your Own Package

Run the following:

```sh
# log in to npm
npm login

# publish a package
npm publish ./the-most-fancy-package-ever
```

## Use the Published Package

Edit `./app/src/package.json` to rely on your package. Then run the following to see what happens:

```sh
# in fish
docker run -it (docker build ./app -q)

# in bash
docker run -it $(docker build ./app -q)
```
