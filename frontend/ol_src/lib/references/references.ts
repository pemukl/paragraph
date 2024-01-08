// write a typescript class that represents the structure of the above JSON
// and write a function that takes the above JSON and returns an instance of the class

export class Reference {
  text!: string;
  url!: string;
}

export function referenceFromJson(json: {
  type: string;
  text?: string;
  content?: string;
  url: string;
}): Reference {
  const reference = new Reference();
  reference.text = "no text found";
  if(json.text){
    reference.text = json.text;
  }
  if(json.content) {
    reference.text = json.content;
  }
  reference.url = json.url;
  return reference;
}
