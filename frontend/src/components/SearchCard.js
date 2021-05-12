import { Link } from "react-router-dom";

import moment from 'moment';


const SearchCard = (props) => {
    return (
        <Link className="bg-gray-100 rounded-sm pt-5 px-5 text-left shadow hover:shadow-md" to={props.href}>
            <p className="mb-3 text-center">
                {props.numberOfTweets} tweets about
                <span className="font-semibold italic text-blue-900"> {props.searchTerm} </span>
                were classified
            </p>
            <p className="text-right mb-2 text-gray-500 font-semibold">
                {moment(props.date).format('MMMM Do, YYYY · HH:mm')}
            </p>
        </Link>
    );
}

export default SearchCard;
