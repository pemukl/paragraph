import { MongoClient } from "mongodb";
import type { RequestEvent } from "./$types";

export async function GET({ url }: RequestEvent) {
    const lawID: string = url.searchParams.get('lawID') ?? 'No ID provided';

    try {

        const mongoUri = process.env.MONGO_URI ?? 'mongodb://root:publicpw@localhost:27017';


        const client = new MongoClient(mongoUri);
        await client.connect();

        // Specify the database and collection
        const db = client.db("laws");
        const collection = db.collection("de");

        //enumerate all documents in the collection

        // Fetch the document based on the provided lawID
        const result = await collection
            .findOne({"abbreviation" : lawID} );

        // Close the MongoDB connection
        await client.close();

        if (result) {
            console.log("Fetched " + lawID + " from " + mongoUri);
            return new Response(JSON.stringify(result));
        } else {
            console.log(`Law with ID ${lawID} not found`);
            return new Response('Law not found', { status: 404 });
        }
    } catch (error) {
        console.error(error);
        return new Response('Internal Server Error', { status: 500 });
    }
}
