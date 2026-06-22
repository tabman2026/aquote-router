# When To Release

Default for documentation-only work: do not release a new package version.

## 不发版本

Do not release when the change is only:

1. a temporary live source failure;
2. a local pytdx server pool timeout;
3. a local report refresh;
4. a log-only change;
5. a typo in docs that does not affect the PyPI page.

## patch

Release a patch version when users need a fixed package for:

1. package code bugs;
2. CLI startup failure;
3. import failure;
4. public documentation that seriously misleads users;
5. schema guard allowing invalid data;
6. unit conversion errors.

## minor

Release a minor version when the package adds:

1. a new adapter;
2. a new public API;
3. a new public CLI command;
4. a new public return field;
5. a compatible source policy expansion.

## Task 023 Decision

This task adds developer documentation and tests only. It should not create a
tag and should not publish a package. A future patch release is only needed if
the PyPI page must show the new developer entry or if package data changes are
required for installed documentation access.

