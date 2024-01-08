import fs from 'fs';


export async function load({ params }) {

    //create a list of all files in the law directory
    let files = fs.readdirSync("src/lib/law/");

    //remove the .json extension from each file
    files = files.filter((value) => (value.endsWith(".json"))).map((file) => {
        return file.replace(".json", "");
    });

    return {"laws":files};

}
