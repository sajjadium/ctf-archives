import Link from 'next/link';
import Image from 'next/image';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faKey } from "@fortawesome/free-solid-svg-icons";

type ContainerProps = {
    studio: boolean;
    id: string;
    name: string;
    pseudo: string;
    chatId: string;
    private: boolean;
};

export default function Video(props: ContainerProps) {
    var isPriv = props.private ? "[Private]" : "";
    var url    = props.studio ? `/video/edit/${props.id}` : `/video/view/${props.id}`

    return (
    <div>
        <Link href={url}>
            <Image src="/img/hero.png" alt="" width={333} height={180} /><br />
        </Link>

        <div className="container">
            <div className="row">
                <div className="three columns">
                    <FontAwesomeIcon icon={faUser} size="lg" />
                </div>
                <div className="nine columns" style={{ textAlign: "left", fontWeight: "bold"}}>
                    {isPriv} {props.name}
                </div>
            </div>
            <div className="row">
                <div className="three columns">&nbsp;</div>
                <div className="nine columns" style={{ textAlign: "left" }}>
                    {props.pseudo}
                </div>
            </div>
        </div>
    </div>
    );
}