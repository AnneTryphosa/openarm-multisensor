import numpy as np
import cv2
from scipy.interpolate import RectBivariateSpline
from multiprocessing.dummy import Pool as ThreadPool


def multi_point_lucas_kanade(curr_image, template_image, point_mappings, eps, max_iters, pyr_levels):
    # convert points into tuples of arguments for op for multithreading
    tup_converts = [(point_mapping, curr_image, template_image, eps, max_iters, pyr_levels) for point_mapping in point_mappings]
    # open ten threads
    pool = ThreadPool(10)
    # run LK with multiple threads, return result
    ret = pool.starmap(update_point, tup_converts)
    # close threads
    pool.close()
    return ret
    # ret = []
    # for point_mapping in point_mappings:
    #     point = point_mapping[0]
    #     associated_points = point_mapping[1]
    #     warp_params = lucas_kanade_affine_warp(curr_image, template_image, associated_points[0], associated_points[1], eps, max_iters)
    #     new_point = affine_warp_single_point(point, warp_params)
    #     new_Xs, new_Ys = affine_warp_point_set(associated_points[0], associated_points[1], warp_params)
    #     ret.append((new_point, (new_Xs, new_Ys)))
    #
    # return ret



def update_point(point_mapping, curr_image, template_image, eps, max_iters, pyr_levels):
    # x, y numpy array
    point = point_mapping[0]
    # tuple of X, Y points (template)
    associated_points = point_mapping[1]
    warp_params = pyramidal_lucas_kanade_affine_warp(curr_image, template_image, associated_points[0], associated_points[1], eps,
                                           max_iters, pyr_levels)
    new_point = affine_warp_single_point(point, warp_params)
    new_Xs, new_Ys = affine_warp_point_set(associated_points[0], associated_points[1], warp_params)
    return (new_point, (new_Xs, new_Ys))


def pyramidal_lucas_kanade_affine_warp(curr_image, template_image, X, Y, eps, max_iters, pyr_levels):
    curr_image_pyramids = []
    template_image_pyramids = []

    curr_image_pyramids.append(curr_image)
    template_image_pyramids.append(template_image)

    for i in range(pyr_levels):
        curr_image_rows, curr_image_cols = map(int, curr_image_pyramids[i].shape)
        template_image_rows, template_image_cols = map(int, template_image_pyramids[i].shape)
        curr_image_pyramids.append(cv2.pyrDown(curr_image_pyramids[i], dstsize=(curr_image_cols // 2, curr_image_rows // 2)))
        template_image_pyramids.append(cv2.pyrDown(template_image_pyramids[i], dstsize=(template_image_cols // 2, template_image_rows // 2)))


    warp_params = np.zeros(6)

    for i in range(len(template_image_pyramids) - 1, -1, -1):
        print('PYRAMID LEVEL: ', i)

        curr_image_pyramid = curr_image_pyramids[i]
        template_image_pyramid = template_image_pyramids[i]
        X_pyr = X // (2 ** i)
        Y_pyr = Y // (2 ** i)
        print('IMAGE SHAPE: ', curr_image_pyramid.shape)
        print('X_pyr, Y_pyr: ', X_pyr[0][0], Y_pyr[0][0])

        warp_params = lucas_kanade_affine_warp(curr_image_pyramid, template_image_pyramid, warp_params, X_pyr, Y_pyr, eps, max_iters)

    return warp_params



def lucas_kanade_affine_warp(curr_image, template_image, warp_params, X, Y, eps, max_iters):

    print("STARTING")
    print("")
    print("")

    update_warp_params = warp_params.copy()


    num_params = len(update_warp_params)

    # spline interpolation of image for potential indexing into non-integer coordinates
    spline_inter_curr_image = RectBivariateSpline(np.arange(curr_image.shape[0]), np.arange(curr_image.shape[1]), curr_image)
    spline_inter_template_image = RectBivariateSpline(np.arange(template_image.shape[0]), np.arange(template_image.shape[1]), template_image)

    iter = 0
    restart_descent = False
    while (True):

        print(update_warp_params)

        # unpack warp parameters
        p1 = update_warp_params[0]
        p2 = update_warp_params[1]
        p3 = update_warp_params[2]
        p4 = update_warp_params[3]
        p5 = update_warp_params[4]
        p6 = update_warp_params[5]

        # mesh grid of x, y coordinates of template window
        # X, Y = np.meshgrid(x_coords, y_coords)

        # grid of warped x, y coordinates
        X_w = (1 + p1) * X + p3 * Y + p5
        Y_w = p2 * X + (1 + p4) * Y + p6

        # get indeces of warped points which do not go out of bounds in curr_image
        valid_pos = (X_w >= 0) & (X_w < curr_image.shape[1]) & (Y_w >= 0) & (Y_w < curr_image.shape[1])

        # filter out out of bounds points, flatten for both original and warped
        X_w = X_w[valid_pos].flatten()
        Y_w = Y_w[valid_pos].flatten()

        X_filtered = X[valid_pos].flatten()
        Y_filtered = Y[valid_pos].flatten()


        # template image points at valid coordinates
        template_image_values = spline_inter_template_image.ev(Y_filtered, X_filtered).flatten()

        # image points at valid warped coordinates
        warped_image_values = spline_inter_curr_image.ev(Y_w, X_w).flatten()

        error_image = template_image_values - warped_image_values

        # gradient computations at warped points for curr image
        # TODO: check if ordering of dx, dy correct
        delIx_warped = spline_inter_curr_image.ev(Y_w, X_w, dx = 0, dy = 1).flatten()
        delIy_warped = spline_inter_curr_image.ev(Y_w, X_w, dx = 1, dy = 0).flatten()

        num_valid_points = X_filtered.shape[0]

        # go through points and compute hessian, steepest descent image
        hessian = np.zeros((num_params, num_params))
        steepest_descent_image = np.zeros(num_params)
        for i in range(num_valid_points):
            x = X_filtered[i]
            y = Y_filtered[i]
            error = error_image[i]
            del_x = delIx_warped[i]
            del_y = delIy_warped[i]
            vec = np.array([x * del_x, x * del_y, y * del_x, y * del_y, del_x, del_y])
            steepest_descent_image += vec * error
            hessian += np.dot(vec.reshape(num_params, 1), vec.reshape(1, num_params))

        delta_p = np.dot(np.linalg.pinv(hessian), steepest_descent_image)
        # print('Delta p norm: ', np.linalg.norm(delta_p))

        # take a descent step
        update_warp_params += delta_p

        if (np.linalg.norm(delta_p) <= eps):
            break

        iter += 1

        if (iter > max_iters):
            restart_descent = True
            break

    if restart_descent:
        iter = 0
        update_warp_params = np.zeros(6)
        while (iter <= 1000):

            print(update_warp_params)

            # unpack warp parameters
            p1 = update_warp_params[0]
            p2 = update_warp_params[1]
            p3 = update_warp_params[2]
            p4 = update_warp_params[3]
            p5 = update_warp_params[4]
            p6 = update_warp_params[5]

            # mesh grid of x, y coordinates of template window
            # X, Y = np.meshgrid(x_coords, y_coords)

            # grid of warped x, y coordinates
            X_w = (1 + p1) * X + p3 * Y + p5
            Y_w = p2 * X + (1 + p4) * Y + p6

            # get indeces of warped points which do not go out of bounds in curr_image
            valid_pos = (X_w >= 0) & (X_w < curr_image.shape[1]) & (Y_w >= 0) & (Y_w < curr_image.shape[1])

            # filter out out of bounds points, flatten for both original and warped
            X_w = X_w[valid_pos].flatten()
            Y_w = Y_w[valid_pos].flatten()

            X_filtered = X[valid_pos].flatten()
            Y_filtered = Y[valid_pos].flatten()

            # template image points at valid coordinates
            template_image_values = spline_inter_template_image.ev(Y_filtered, X_filtered).flatten()

            # image points at valid warped coordinates
            warped_image_values = spline_inter_curr_image.ev(Y_w, X_w).flatten()

            error_image = template_image_values - warped_image_values

            # gradient computations at warped points for curr image
            # TODO: check if ordering of dx, dy correct
            delIx_warped = spline_inter_curr_image.ev(Y_w, X_w, dx=0, dy=1).flatten()
            delIy_warped = spline_inter_curr_image.ev(Y_w, X_w, dx=1, dy=0).flatten()

            num_valid_points = X_filtered.shape[0]

            # go through points and compute hessian, steepest descent image
            hessian = np.zeros((num_params, num_params))
            steepest_descent_image = np.zeros(num_params)
            for i in range(num_valid_points):
                x = X_filtered[i]
                y = Y_filtered[i]
                error = error_image[i]
                del_x = delIx_warped[i]
                del_y = delIy_warped[i]
                vec = np.array([x * del_x, x * del_y, y * del_x, y * del_y, del_x, del_y])
                steepest_descent_image += vec * error
                hessian += np.dot(vec.reshape(num_params, 1), vec.reshape(1, num_params))

            delta_p = np.dot(np.linalg.pinv(hessian), steepest_descent_image)
            # print('Delta p norm: ', np.linalg.norm(delta_p))

            # take a descent step
            update_warp_params += delta_p

            if (np.linalg.norm(delta_p) <= eps):
                break

            iter += 1


    print("ENDING")
    print("")
    print("")

    return update_warp_params

def affine_warp_point_set(x_coords, y_coords, warp_params):
    # unpack warp parameters
    p1 = warp_params[0]
    p2 = warp_params[1]
    p3 = warp_params[2]
    p4 = warp_params[3]
    p5 = warp_params[4]
    p6 = warp_params[5]

    x_coords_ret = (1 + p1) * x_coords + p3 * y_coords + p5
    y_coords_ret = p2 * x_coords + (1 + p4) * y_coords + p6

    return x_coords_ret, y_coords_ret

def affine_warp_single_point(point, warp_params):
    # unpack warp parameters
    p1 = warp_params[0]
    p2 = warp_params[1]
    p3 = warp_params[2]
    p4 = warp_params[3]
    p5 = warp_params[4]
    p6 = warp_params[5]
    x = point[0]
    y = point[1]

    new_x = (1 + p1) * x + p3 * y + p5
    new_y = p2 * x + (1 + p4) * y + p6
    return np.array([new_x, new_y])
