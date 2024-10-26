import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser } from "@fortawesome/free-solid-svg-icons";
import parseMarkdown from "../helpers/utils/parseMarkdown";

type ContainerProps = {
    content: string;
    pseudo: string;
};

export default function Message(props: ContainerProps) {
    const msg = parseMarkdown(props.content);

    return (
    <div className="mb-20">
        <FontAwesomeIcon icon={faUser} className="mr-10" /> <span dangerouslySetInnerHTML={{ __html: `${props.pseudo} ${msg}` }}></span>
    </div>
    );
}