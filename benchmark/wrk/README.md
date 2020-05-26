1. install wrk
```sh
brew install wrk
```
2. generate json like [sample.json](sample.json)
3. run test
```sh
wrk -t <thread> -c <connection> -d <duration> --timeout <timeout>  -s ./benchmark.lua --latency <host>
```
