import styled from "@emotion/styled";

const StoryCard = styled.div<{ backgroundImage: string }>`
  width: 500px;
  height: 800px;
  position: relative;
  border: 1px solid black;
  border-radius: 8px;
  box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.1);

  background-image: url(${(props) => props.backgroundImage});
  background-size: 100% 100%;
`;

const StoryID = styled.div`
  font-size: 12px;
  position: absolute;
  right: 0;
  top: 0;
  padding: 4px;
  background-color: black;
  color: white;
`;

const StoryText = styled.h2`
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 48px;
  word-break: break-all;
`;

const StoryAction = styled.button`
  box-sizing: border-box;
  width: 200px;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  color: black;
  background: white;
  border-radius: 4px;

  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
`;

export function RenderStory(props: {
  story: {
    id: number;
    text: string;
    action: string;
    image: { url: string };
  };
  fields: Record<string, string>;
}) {
  const template = props.story.text;
  const text = props.fields
    ? template.replace(/{{(.*?)}}/g, (_, key) => props.fields[key] ?? "")
    : template;
  return (
    <StoryCard
      id="story-card"
      backgroundImage={"/api"+props.story.image.url}
    >
      <StoryID>ID: {props.story.id}</StoryID>
      <StoryText>{text}</StoryText>
      <StoryAction>{props.story.action}</StoryAction>
    </StoryCard>
  );
}
