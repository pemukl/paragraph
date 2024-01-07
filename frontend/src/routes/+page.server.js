import { MongoClient } from "mongodb";


export async function load() {
    const mongoUri = "mongodb://root:publicpw@localhost:27017"
    //create a list of all laws in the database "laws" and collection "de"
    const collection = (await MongoClient.connect(mongoUri))
        .db("laws").collection("de");

    // map every entry in the collection its "abbreviation"
    const laws = await collection.find().map((entry) => entry.abbreviation).toArray();

    return {"laws":laws};

}
