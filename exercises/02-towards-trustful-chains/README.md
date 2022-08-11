# Towards Trustful Software Supply Chains

## Three Challenges

SLSA represents a supply chain as a DAG of sources, builds, dependencies, and packages. One artifact’s supply chain is a combination of its dependencies’ supply chains plus its own sources and builds.

![From SLSA Version 1](https://slsa.dev/images/supply-chain-model.svg)

Based upon this idea, we can divide-and-conquer problems we're running into on constructing a trustful software supply chain as follows:

- **Problems on establishing _trust on first use of dependencies_**
- **Problems on establishing _trust on continuous use of dependencies_**
- **Problems on establishing _a trustful process to supply one's own source to consumers_**

## Establish Trust on First Use of Dependencies

Since we're an acquirer in a software supply chain, the way we depend on others matters.

Establishing trust on a first use is a big challenge for us, and this is where many developers have interests. It literally involves with daily workflows of modern developers ― they execute `yarn add <name>`, modify `go.mod`, or `cargo add`, with a slight worry. Few developers review codes on adding new package dependencies or adding tools to CI workflows, much less on updating existing dependencies.

Here's a list of possible solutions to establish a first trust:

- **Depend on what you yourself have reviewed**
  - From the viewpoint of package ecosystems, it's important to keep what we can review easily is what we'll use; see [a recent activity in this line by npm](https://github.com/npm/rfcs/pull/626).
  - From the viewpoint of package users, we need to be as aware as possible.
- **Depend on what someone has reviewed**
  - [Assured Open Source Software service by Google](https://cloud.google.com/blog/products/identity-security/introducing-assured-open-source-software-service) or [Alpha-Omega Project](https://openssf.org/community/alpha-omega/) might help

## Establish Trust on Continuous Use of Dependencies

Even if we succeed in depending on only trustworthy artifacts, we still need to ensure what we're depending on are _what we decided to trust at the point in time_. At least we need to:

- **Define dependencies statically to lock them (like `go.sum`)**
- **Use locked dependencies following the definition properly**

Another challenge is that compiled binaries or containers often lack information on what it is depending on internally, resulting in operation challenges. Suppose that you see a news that a researcher found that `package-blah-blah` had included malwares. Once you forget what kind of tools and packages container images depends on, you'll give a big sigh and lose time. This is one of the reasons why we need to have Software Bill of Materials (SBoM).

## Establishing a Trustful Process to Supply Things

Since we're at once acquirer and supplier, a process to ship things from developers to consumers matters much. To make the artifacts reliable, it'd be good to have:

- Well-organized source code management (SCM)
  - cf. ["Source requirements" by SLSA](https://slsa.dev/spec/v0.1/requirements#source-requirements)
- Well-organized CI/CD pipelines
  - cf. ["Build requirements" by SLSA](https://slsa.dev/spec/v0.1/requirements#build-requirements)
- Well-organized artifact management
- Well-organized delivery of artifacts

The process could be designed from the viewpoint of:

- decreasing risks for minimize damages
- increasing auditability for fast incident response
  - cf. ["Provenance requirements" by SLSA](https://slsa.dev/spec/v0.1/requirements#provenance-requirements)

## Overview of Chapter 03-08

You'll review each of aforementioned three challenges as follows:

- **problems on establishing _trust on first use of dependencies_**
  - N/A
- **problems on establishing _trust on continuous use of dependencies_**
  - [../04-hardening-builds](../04-hardening-builds)
  - [../06-hardening-delivery](../06-hardening-delivery)
- **problems on establishing _a trustful process to supply one's own source to consumers_**
  - on decreasing risks of the whole process
    - refer to #seccamp2022b4.
  - on increasing auditability of the whole process:
    - [../03-hardening-scm](../03-hardening-scm)
    - [../04-hardening-builds](../04-hardening-builds)
    - [../04-hardening-artifacts](../05-hardening-artifacts)
    - [../06-hardening-delivery](../06-hardening-delivery)
