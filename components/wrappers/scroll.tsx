import { useEffect, ComponentType } from "react";

export interface WithScolledProps {}
// Hide the menu unless at the top or bottom of the page

/**
 * Wrap a component with a listener for scrolling to the top or bottom of the page
 * @param Component The component to wrap
 * @param on_boundary_hit The callback to call when the user scrolls to the top or bottom of the page
 * @param on_boundary_leave The callback to call when the user scrolls away from the top or bottom of the page
 * @param boundary_tolerance How many pixels around the top and bottom of the page to call the callbacks for
 * @returns The wrapped component
 */
const with_scroll_cbs = <Props extends object>(
  Component: ComponentType<Props>,
  on_boundary_hit: () => void,
  on_boundary_leave: () => void,
  boundary_tolerance: number = 100
): ComponentType<Props & WithScolledProps> => {
  const handle_scroll = () => {
    // How many pixels around the top and bottom to show the navbar for
    const current_position = window.pageYOffset;
    const max_position = document.body.scrollHeight - window.innerHeight;
    const below_top = current_position > boundary_tolerance;
    const at_bottom = current_position >= max_position - boundary_tolerance;
    if (below_top && !at_bottom) return on_boundary_leave();
    on_boundary_hit();
  };
  return (props) => {
    useEffect(() => {
      document.addEventListener("scroll", handle_scroll);
      return () => document.removeEventListener("scroll", handle_scroll);
    });
    return <Component {...props} />;
  };
};

export default with_scroll_cbs;
