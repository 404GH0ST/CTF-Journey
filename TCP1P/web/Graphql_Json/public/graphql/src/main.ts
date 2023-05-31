import { serve } from "http"
import { Yoga } from "./controllers/resolver.ts"
import { User } from "./models/db.ts"


serve(Yoga, {
    async onListen({ hostname, port }) {
        try {
            await new User({
                username: "SecureUsernameThatIUseInEveryAccount",
                password: Deno.readTextFileSync("./flag.txt"),
            }).save()
        } catch (e) {
            console.error(e)
        }

        console.log(`Listening on http://${hostname}:${port}/graphql`)
    }
})