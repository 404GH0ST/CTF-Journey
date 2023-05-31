import { connect, model, Schema } from "mongoose"
import { DB_URL } from "config"
import { type IUser } from "./types.d.ts"

await connect(DB_URL)

const userSchema = new Schema<IUser>({
    username: { type: String, required: true, unique: true },
    password: { type: String, required: true },
})

export const User = model("User", userSchema)