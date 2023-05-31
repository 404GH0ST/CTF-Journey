import { User } from "../models/db.ts"
import { IUser } from "../models/types.d.ts"
import { createSchema, createYoga } from "graphql-yoga"

export const Yoga = createYoga({
    schema: createSchema({
        typeDefs: Deno.readTextFileSync("./models/schema.gql"),
        resolvers: {
            Query: {
                info: () => "Ingfo ingfo...",
                getUser: (_, { data }: { data: IUser }): Promise<IUser> => {
                    return new Promise((resolve, reject) => {
                        User.findOne({ username: data.username }, (err: Error, user: IUser) => {
                            if (err) {
                                return reject(err)
                            }
                            return resolve(user)
                        })
                    })
                }
            },
        }
    }),
})